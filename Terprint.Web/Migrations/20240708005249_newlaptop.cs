using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class newlaptop : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Grower",
                columns: table => new
                {
                    GrowerId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Grower", x => x.GrowerId);
                });

            migrationBuilder.CreateTable(
                name: "Matrixes",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Terpene = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Matrix = table.Column<int>(type: "int", nullable: false),
                    Row = table.Column<int>(type: "int", nullable: false),
                    Column = table.Column<int>(type: "int", nullable: false),
                    Color = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Matrixes", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "RatingCategory",
                columns: table => new
                {
                    RatingCategoryId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RatingCategoryType = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CategoryName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CategoryDescription = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CategoryTitle = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_RatingCategory", x => x.RatingCategoryId);
                });

            migrationBuilder.CreateTable(
                name: "States",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    StateName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateAbbreviation = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateCapital = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateRegion = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_States", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Strain",
                columns: table => new
                {
                    StrainId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    StrainName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StrainDescription = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Strain", x => x.StrainId);
                });

            migrationBuilder.CreateTable(
                name: "GrowerStates",
                columns: table => new
                {
                    GrowersGrowerId = table.Column<int>(type: "int", nullable: false),
                    StatesId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GrowerStates", x => new { x.GrowersGrowerId, x.StatesId });
                    table.ForeignKey(
                        name: "FK_GrowerStates_Grower_GrowersGrowerId",
                        column: x => x.GrowersGrowerId,
                        principalTable: "Grower",
                        principalColumn: "GrowerId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_GrowerStates_States_StatesId",
                        column: x => x.StatesId,
                        principalTable: "States",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Batch",
                columns: table => new
                {
                    BatchId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Date = table.Column<DateOnly>(type: "date", nullable: false),
                    GrowerID = table.Column<int>(type: "int", nullable: true),
                    StrainID = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Batch", x => x.BatchId);
                    table.ForeignKey(
                        name: "FK_Batch_Grower_GrowerID",
                        column: x => x.GrowerID,
                        principalTable: "Grower",
                        principalColumn: "GrowerId");
                    table.ForeignKey(
                        name: "FK_Batch_Strain_StrainID",
                        column: x => x.StrainID,
                        principalTable: "Strain",
                        principalColumn: "StrainId");
                });

            migrationBuilder.CreateTable(
                name: "Rating",
                columns: table => new
                {
                    RatingId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Growerid = table.Column<int>(type: "int", nullable: false),
                    userid = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    RatingCategoryID = table.Column<int>(type: "int", nullable: false),
                    Value = table.Column<int>(type: "int", nullable: false),
                    Notes = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    BatchID = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Rating", x => x.RatingId);
                    table.ForeignKey(
                        name: "FK_Rating_Batch_BatchID",
                        column: x => x.BatchID,
                        principalTable: "Batch",
                        principalColumn: "BatchId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Rating_RatingCategory_RatingCategoryID",
                        column: x => x.RatingCategoryID,
                        principalTable: "RatingCategory",
                        principalColumn: "RatingCategoryId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "TerpeneValues",
                columns: table => new
                {
                    TerpeneValueId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Value = table.Column<double>(type: "float", nullable: false),
                    TerpeneName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    BatchID = table.Column<int>(type: "int", nullable: false),
                    Scale = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TerpeneValues", x => x.TerpeneValueId);
                    table.ForeignKey(
                        name: "FK_TerpeneValues_Batch_BatchID",
                        column: x => x.BatchID,
                        principalTable: "Batch",
                        principalColumn: "BatchId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "THCValues",
                columns: table => new
                {
                    THCValueId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BatchID = table.Column<int>(type: "int", nullable: false),
                    Analyte = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Dilution = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LOD = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LOQ = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Result = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Percent = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_THCValues", x => x.THCValueId);
                    table.ForeignKey(
                        name: "FK_THCValues_Batch_BatchID",
                        column: x => x.BatchID,
                        principalTable: "Batch",
                        principalColumn: "BatchId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Batch_GrowerID",
                table: "Batch",
                column: "GrowerID");

            migrationBuilder.CreateIndex(
                name: "IX_Batch_StrainID",
                table: "Batch",
                column: "StrainID");

            migrationBuilder.CreateIndex(
                name: "IX_GrowerStates_StatesId",
                table: "GrowerStates",
                column: "StatesId");

            migrationBuilder.CreateIndex(
                name: "IX_Rating_BatchID",
                table: "Rating",
                column: "BatchID");

            migrationBuilder.CreateIndex(
                name: "IX_Rating_RatingCategoryID",
                table: "Rating",
                column: "RatingCategoryID");

            migrationBuilder.CreateIndex(
                name: "IX_TerpeneValues_BatchID",
                table: "TerpeneValues",
                column: "BatchID");

            migrationBuilder.CreateIndex(
                name: "IX_THCValues_BatchID",
                table: "THCValues",
                column: "BatchID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "GrowerStates");

            migrationBuilder.DropTable(
                name: "Matrixes");

            migrationBuilder.DropTable(
                name: "Rating");

            migrationBuilder.DropTable(
                name: "TerpeneValues");

            migrationBuilder.DropTable(
                name: "THCValues");

            migrationBuilder.DropTable(
                name: "States");

            migrationBuilder.DropTable(
                name: "RatingCategory");

            migrationBuilder.DropTable(
                name: "Batch");

            migrationBuilder.DropTable(
                name: "Grower");

            migrationBuilder.DropTable(
                name: "Strain");
        }
    }
}
